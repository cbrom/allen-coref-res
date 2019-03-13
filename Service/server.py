import grpc
from concurrent import futures
import time

import coref_pb2
import coref_pb2_grpc

import coref_res_allen


class CorefResolvServicer(coref_pb2_grpc.CorefResolvServicer):
    def resolve(self, request, context):
        if request.document is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("document is empty")
            return coref_pb2.Output()

        elif request.document == "":
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("document is required")
            return coref_pb2.Output()

        response = coref_pb2.Output()

        result = coref_res_allen.CoreferenceResolver.coref_resolution(request.document)

        # top_spans
        top_span = response.top_spans.add()
        for s, e in result['top_spans']:
            top_span_index = top_span.top_span_pair.add()
            top_span_index.index_start = s
            top_span_index.index_end = e

        # predicted_antecedents
        predicted_antecedent = response.predicted_antecedents.add()
        for val in result['predicted_antecedents']:
            predicted_antecedent.predicted = val

        # document
        document = response.document.add()
        for val in result['document']:
            document.document_token = val

        # clusters
        cluster = response.cluster.add()
        for cluster_res in result['clusters']:
            coref = cluster.corefs.add()
            for s, e in cluster_res:
                coref_pair = coref.corefs_pair.add()
                coref_pair.index_start = s
                coref_pair.index_end = e


        return response

def start_server(port="50051"):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    coref_pb2_grpc.add_CorefResolvServicer_to_server(CorefResolvServicer(), server)
    server.add_insecure_port('[::]' + str(port))
    return server

if __name__ == '__main__':
    server = start_server()
    server.start()
    _ONE_DAY = 86400
    try:
        while True:
            time.sleep(_ONE_DAY)
    except KeyboardInterrupt:
        server.stop()