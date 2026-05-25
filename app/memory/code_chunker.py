class CodeChunker:

    @staticmethod
    def chunk_content(
        content,
        chunk_size=80
    ):

        lines = content.splitlines()

        chunks = []

        for i in range(
            0,
            len(lines),
            chunk_size
        ):

            chunk = "\n".join(
                lines[i:i + chunk_size]
            )

            chunks.append(chunk)

        return chunks