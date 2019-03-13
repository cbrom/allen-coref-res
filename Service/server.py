import grpc
from concurrent import futures
import time

import coref_pb2
import coref_pb2_grpc

import coref_res_allen


class CorefResolvServicer(coref_pb2_grpc.CorefResolutionServicer):
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
        top_spans_list = []
        for s, e in result['top_spans']:
            pair = coref_pb2.IndexPair(s=s, e=e)
            top_spans_list.append(pair)
        
        clusters_list = []
        for clusters_res in result['clusters']:
            cluster_list = []
            for s, e in clusters_res:
                pair = coref_pb2.IndexPair(s=s, e=e)
                cluster_list.append(pair)
            cluster = coref_pb2.Cluster(pairs=cluster_list)
            clusters_list.append(cluster)

        top_spans = coref_pb2.TopSpans(pairs=top_spans_list)

        response = coref_pb2.Output(
            top_spans = top_spans, predicted_antecedents = result['predicted_antecedents'], 
            document = result['document'], clusters = clusters_list
        )

        return response

def start_server(port="50051"):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    coref_pb2_grpc.add_CorefResolutionServicer_to_server(CorefResolvServicer(), server)
    server.add_insecure_port('localhost:' + str(port))
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