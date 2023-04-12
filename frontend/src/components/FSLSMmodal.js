import "react-day-picker/dist/style.css";
import { useEffect, useState } from "react";
import { useRecoilState } from "recoil";
import { ErrorAtom, FSLSMQuestionModalAtom } from "../atoms";
import { useMutation, useLazyQuery } from "@apollo/client";
import { FSLSMQuestions, AddFSLSMquestionsResponse } from "../gql";
import { Loading } from "./Loading";

export const FSLSMQuestionModal = () => {
	const [data, setData] = useState(null);
	const [loading, setLoading] = useState(false);
	const [answered, setAnswered] = useState([]);
	const [err, setErr] = useRecoilState(ErrorAtom);
	const [getFSLSMQuestionModalActive, setFSLSMQuestionModalActive] =
		useRecoilState(FSLSMQuestionModalAtom);

	const [getQuestions] = useLazyQuery(FSLSMQuestions, {
		onCompleted: (response) => {
			setData(response.fslsmQuestions);
		},
		onError: (error) => {
			setErr(error.message);
		},
	});

	const [setFslsmquestionsResponse] = useMutation(
		AddFSLSMquestionsResponse,
		{
			onCompleted: (data) => {
				if (
					data.addFslsmquestionsResponse &&
					data.addFslsmquestionsResponse.success
				)
					setFSLSMQuestionModalActive(false);
			},
			onError: (error) => {
				setErr(error.message);
			},
		}
	);
	useEffect(() => {
		getQuestions();
	}, []);

	const onSubmit = () => {
		if (answered.length !== 10) return setErr("Fill the form fully");
		setFslsmquestionsResponse({
			variables: { res: answered },
		});
	};
	return (
		<div
			className={`modal ${
				getFSLSMQuestionModalActive ? "is-active" : ""
			}`}>
			<div className="modal-background"></div>
			<div className="modal-content">
				<section className="box">
					{loading ? (
						<Loading />
					) : (
						<>
							<p className="field is-size-3">
								Tell us, How do you prefer to learn?
							</p>
							{data ? (
								data.map((e) => (
									<div
										className="field"
										key={e.order}>
										<label className="label">
											{e.text}
										</label>
										<div
											className="control"
											onChange={(e) => {
												const arr =
													e.target.value.split(
														","
													);
												let temp =
													answered.filter(
														(e) =>
															e.question !==
															parseInt(
																arr[0]
															)
													);
												temp.push({
													question:
														parseInt(
															arr[0]
														),
													answer: arr[1],
												});
												setAnswered(temp);
											}}>
											<div className="block">
												<label className="radio">
													<input
														type="radio"
														name={`question-${e.order}`}
														value={`${e.order},${e.choices[0].id}`}
													/>
													{
														e
															.choices[0]
															.text
													}
												</label>
											</div>
											<div className="block">
												<label className="radio">
													<input
														type="radio"
														name={`question-${e.order}`}
														value={`${e.order},${e.choices[1].id}`}
													/>
													{
														e
															.choices[1]
															.text
													}
												</label>
											</div>
										</div>
									</div>
								))
							) : (
								<></>
							)}
							<div className="field is-horizontal">
								<div className="field-label is-normal">
									<button
										className="button is-primary"
										onClick={() => onSubmit()}>
										Submit
									</button>
								</div>
							</div>
						</>
					)}
				</section>
			</div>
			<button
				onClick={() => setFSLSMQuestionModalActive(false)}
				className="modal-close is-large"
				aria-label="close"></button>
		</div>
	);
};
