import "react-day-picker/dist/style.css";
import { useEffect, useState } from "react";
import { useRecoilState } from "recoil";
import { ErrorAtom, FSLSMQuestionModalAtom } from "../atoms";
import { useMutation, useQuery } from "@apollo/client";
import { FSLSMQuestions, AddFSLSMquestionsResponse } from "../gql";
import { Loading } from "./Loading";

export const FSLSMQuestionModal = () => {
	const [answered, setAnswered] = useState([]);
	const [err, setErr] = useRecoilState(ErrorAtom);
	const [getFSLSMQuestionModalActive, setFSLSMQuestionModalActive] =
		useRecoilState(FSLSMQuestionModalAtom);

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
	const { loading, error, data } = useQuery(FSLSMQuestions);

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
								data.fslsmQuestions.map((e) => (
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
											<label className="radio">
												<input
													type="radio"
													name={`question-${e.order}`}
													value={`${e.order},${e.choices[0].id}`}
												/>
												{e.choices[0].text}
											</label>
											<label className="radio">
												<input
													type="radio"
													name={`question-${e.order}`}
													value={`${e.order},${e.choices[1].id}`}
												/>
												{e.choices[1].text}
											</label>
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
