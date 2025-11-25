import argparse

from labeling.labeling_utils.errors_analysis import measure_agreement, create_final_result


parser = argparse.ArgumentParser(description="Measure agreement")
parser.add_argument("--result-folder", type=str, required=False)
parser.add_argument("--label-type", type=str, required=True)
parser.add_argument("--agreement-folder", type=str, required=False)
parser.add_argument("--prompt-round", type=int, required=False)
parser.add_argument("--sample", type=int, required=False)
parser.add_argument("--flag", type=bool, required=False, default=True)
parser.add_argument("--result-path", type=str, required=False)
parser.add_argument("--differently-labelled-data-path", type=str, required=False)


if __name__ == "__main__":
    args = parser.parse_args()

    if args.flag:
        measure_agreement(
            result_folder=args.result_folder,
            label_type=args.label_type,
            agreement_folder=args.agreement_folder,
            prompt_round=args.prompt_round,
            sample=args.sample
        )
    else:
        create_final_result(
            result_path = args.result_folder, 
            differently_labelled_data_path=args.differently_labelled_data_path,
            label_type=args.label_type
        )
