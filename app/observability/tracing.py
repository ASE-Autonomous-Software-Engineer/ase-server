from opentelemetry import trace

tracer = trace.get_tracer(__name__)

class TraceManager:

    @staticmethod
    def start_span(name: str):

        return tracer.start_as_current_span(name)