#!/usr/bin/env python3
# remote_test.py

import asyncio
import logging
from typing import AsyncIterator, Dict, Any, Optional

import argparse
import vertexai
from vertexai import agent_engines


def _get_nested(d: Dict[str, Any], path: str, default=None):
    """Safe dotted-path getter for nested dicts."""
    cur = d
    for key in path.split("."):
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


async def call_agent_engine(
    prompt: str,
    project_id: str,
    location: str,
    staging_bucket: str,
    reasoning_engine_id: str,
    user_id: str = "u_456",
) -> AsyncIterator[Dict[str, Any]]:
    """Initialize Vertex AI, create a remote session, and stream a query."""
    vertexai.init(project=project_id, location=location, staging_bucket=staging_bucket)

    remote_agent = agent_engines.get(reasoning_engine_id)
    print(remote_agent, "\nresource name:", remote_agent.resource_name)

    # Create a remote session (required for streaming)
    remote_session = await remote_agent.async_create_session(user_id=user_id)
    session_id = remote_session["id"]
    logging.info("Created session id: %s", session_id)

    # Stream the query
    async for event in remote_agent.async_stream_query(
        user_id=user_id,
        session_id=session_id,
        message=prompt,
    ):
        yield event


async def run_once(
    prompt: str,
    project_id: str,
    location: str,
    staging_bucket: str,
    engine_id: str,
    verbose_events: bool = False,
):
    """Stream once and print a friendly summary at the end."""
    total_score: Optional[int] = None
    artifacts = []  # e.g., ["generated_image_0.png"]
    gcs_uri: Optional[str] = None

    async for ev in call_agent_engine(
        prompt=prompt,
        project_id=project_id,
        location=location,
        staging_bucket=staging_bucket,
        reasoning_engine_id=engine_id,
    ):
        if verbose_events:
            # Be careful: events can be very large; this prints a compact tag.
            kind = (
                _get_nested(ev, "content.parts.0.function_call.name")
                or _get_nested(ev, "content.parts.0.function_response.name")
                or "text/other"
            )
            logging.info("Event kind: %s", kind)

        # Capture artifacts from a function response (e.g., generate_images)
        fr_name = _get_nested(ev, "content.parts.0.function_response.name")
        if fr_name == "generate_images":
            artifact = _get_nested(
                ev, "content.parts.0.function_response.response.artifact_name"
            )
            if artifact:
                artifacts.append(artifact)

        # Some agents also list artifacts in actions.artifact_delta
        ad = _get_nested(ev, "actions.artifact_delta", {})
        if isinstance(ad, dict) and ad:
            artifacts.extend(list(ad.keys()))

        # Capture score if emitted via set_score tool call
        fc_name = _get_nested(ev, "content.parts.0.function_call.name")
        if fc_name == "set_score":
            ts = _get_nested(ev, "content.parts.0.function_call.args.total_score")
            if isinstance(ts, int):
                total_score = ts

        # Capture score and/or GCS URI if placed in state_delta
        state_delta = _get_nested(ev, "actions.state_delta", {})
        if isinstance(state_delta, dict) and state_delta:
            if isinstance(state_delta.get("total_score"), int):
                total_score = state_delta["total_score"]
            # Your tool can set one of these for convenience:
            gcs_uri = (
                gcs_uri
                or state_delta.get("generated_image_gcs_uri")
                or state_delta.get("image_uri")
            )

    # De-dupe artifacts while preserving order
    seen = set()
    artifacts = [a for a in artifacts if not (a in seen or seen.add(a))]

    print("\n=== SUMMARY ===")
    print(f"Prompt: {prompt}")
    print(f"Total Score: {total_score if total_score is not None else 'N/A'}")
    print("Artifacts:", ", ".join(artifacts) if artifacts else "(none reported)")
    if gcs_uri:
        print("GCS URI:", gcs_uri)
    else:
        print(
            "GCS URI: (not provided by agent — download the artifact from the ADK UI "
            "Artifacts tab, or have your tool write to GCS and place the URI in state)"
        )


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default="the-byway-473000-u5")
    parser.add_argument("--location", default="us-central1")
    parser.add_argument("--bucket", default="gs://next-demo-storage1-us-central1")
    parser.add_argument(
        "--engine",
        default="projects/736220893495/locations/us-central1/reasoningEngines/4079051799607115776",
    )
    parser.add_argument("--prompt", default="A cat riding a bicycle")
    parser.add_argument(
        "--verbose-events",
        action="store_true",
        help="Log compact event kinds during the stream",
    )
    args = parser.parse_args()

    try:
        asyncio.run(
            run_once(
                prompt=args.prompt,
                project_id=args.project,
                location=args.location,
                staging_bucket=args.bucket,
                engine_id=args.engine,
                verbose_events=args.verbose_events,
            )
        )
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except Exception as e:
        logging.exception("Error running testclient: %s", e)


if __name__ == "__main__":
    main()
