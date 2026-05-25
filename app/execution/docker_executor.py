import docker

client = docker.from_env()

class DockerExecutor:

    @staticmethod
    def run_in_container(
        image: str,
        command: str,
        working_dir: str
    ):

        container = client.containers.run(
            image=image,
            command=command,
            working_dir="/workspace",
            volumes={
                working_dir: {
                    "bind": "/workspace",
                    "mode": "rw"
                }
            },
            detach=True,
            mem_limit="1g",
            network_disabled=True
        )

        result = container.wait()

        logs = container.logs().decode()

        container.remove()

        return {
            "result": result,
            "logs": logs
        }