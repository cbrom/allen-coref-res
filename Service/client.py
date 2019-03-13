import grpc
import time
import os
import coref_pb2, coref_pb2_grpc


class TestClient():
    def setUp(self):
        self.sentence1 = "Paul was born on January 21, 1953, in Seattle, Washington, to Kenneth Sam Allen and Edna Faye Allen. Allen attended Lakeside School, a private school in Seattle, where he befriended Bill Gates, two years younger, with whom he shared an enthusiasm for computers. Paul and Bill used a teletype terminal at their high school, Lakeside, to develop their programming skills on several time-sharing computer systems."
        self.sentence2 = "The legal pressures facing Michael Cohen are growing in a wide-ranging investigation of his personal business affairs and his work on behalf of his former client, President Trump.  In addition to his work for Mr. Trump, he pursued his own business interests, including ventures in real estate, personal loans and investments in taxi medallions."
        # self.sentence3 = 
        # self.sentence4 = 
        # self.sentence5 = 
        self.port = "50051"
        
        # self.server = create server
        # self.server.start()

    def test_grpc_call(self):
        self.setUp()
        with grpc.insecure_channel('localhost:' + self.port) as channel:
            stub = coref_pb2_grpc.CorefResolutionStub(channel)
            response1 = self.rpc_call(stub, self.sentence1)
            print(response1)
            

    def rpc_call(self, stub, document):
        request = coref_pb2.Input(document=document)
        response = stub.resolve(request)
        return response

if __name__ == "__main__":
    tc = TestClient()
    tc.test_grpc_call()