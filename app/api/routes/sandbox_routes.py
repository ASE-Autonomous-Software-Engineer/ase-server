from fastapi import APIRouter

import docker

router = APIRouter()

client = docker.from_env()

@router.get("/sandbox/containers")

async def get_containers():

    containers = client.containers.list()

    return [
        {
            "id": c.id,
            "name": c.name,
            "status": c.status
        }
        for c in containers
    ]

@router.get("/sandbox/status")

async def sandbox_status():

    return {
        "docker_running": True
    }