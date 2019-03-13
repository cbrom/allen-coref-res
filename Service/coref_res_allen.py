from allennlp .predictors.predictor import Predictor

class CoreferenceResolver:
	# predictor = Predictor.from_path("/root/.allennlp/models/coref-model-2018.02.05.tar.gz")
	predictor = Predictor.from_path("../models/coref-model-2018.02.05.tar.gz")

	def coref_resolution(document):
		return CoreferenceResolver.predictor.predict(document)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--document', '-d', help="Enter the document for coreference resolution")
	args = parser.parse_args()
	if args.document == None:
		print("Please enter the document. Terminating...")
		sys.exit(0)
	print(args.document)

	CoreferenceResolver.coref_resolution(args.document)
