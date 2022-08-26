import csv_parser
import get_data
import predict

def main():
    parsed_data: csv_parser.ParsedContent = csv_parser.parse()
    predict_result: predict.PredictResult = predict.predict(parsedData=parsed_data)
    predict_result.print()

main()