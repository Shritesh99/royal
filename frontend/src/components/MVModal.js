import "react-day-picker/dist/style.css";
import { useEffect, useState } from "react";
import { useRecoilState } from "recoil";
import { ErrorAtom, MVAtom } from "../atoms";
import { useMutation, useLazyQuery } from "@apollo/client";
import { MVQuestions, AddMVQuestions } from "../gql";
import { Loading } from "./Loading";
import mvQuestions from "@/gql/mvQuestions";

export const MVModal = () => {
	const [data, setData] = useState(null);
	const [loading, setLoading] = useState(false);
	const [answered, setAnswered] = useState([]);
	const [err, setErr] = useRecoilState(ErrorAtom);

	const [getMVModalActive, setMVModalActive] = useRecoilState(MVAtom);

	const [getQuestions] = useLazyQuery(MVQuestions, {
		onCompleted: (response) => {
			setData(response.motivationQuestions);
			const arr = Array(response.motivationQuestions.length)
				.fill()
				.map(() => ({
					question: null,
					answer: null,
				}));
			setAnswered(arr);
			setLoading(false);
		},
		onError: (error) => {
			setErr(error.message);
		},
	});

	const [setMVQuestionsResponse] = useMutation(AddMVQuestions, {
		onCompleted: (data) => {
			if (
				data.addMotivationquestionsResponse &&
				data.addMotivationquestionsResponse.success
			)
				setMVModalActive(false);
		},
		onError: (error) => {
			setErr(error.message);
		},
	});
	useEffect(() => {
		getQuestions();
	}, []);

	const onSubmit = () => {
		if (answered.some((e) => e.answer == null))
			return setErr("Fill the form fully");
		setMVQuestionsResponse({
			variables: { res: answered },
		});
	};
	return (
		<div className={`modal ${getMVModalActive ? "is-active" : ""}`}>
			<div className="modal-background"></div>
			<div className="modal-content">
				<section className="box">
					{loading ? (
						<Loading />
					) : (
						<>
							<p className="field is-size-3">
								How motivated are you...
							</p>
							{data ? (
								data.map((e, i) => (
									<div
										className="field"
										key={e.order}>
										<label className="label">
											{e.text}
										</label>
										{i === 0 ? (
											<div
												className="control"
												onChange={(e) => {
													setAnswered([
														{
															question: 1,
															answer: e
																.target
																.value,
														},
														...answered.slice(
															1
														),
													]);
												}}>
												<div className="block">
													<label className="radio">
														<input
															type="radio"
															name={`question-${e.order}`}
															value={
																1
															}
														/>
														Yes
													</label>
													<label className="radio">
														<input
															type="radio"
															name={`question-${e.order}`}
															value={
																0
															}
														/>
														No
													</label>
												</div>
											</div>
										) : (
											<div className="block">
												<input
													class="input is-primary"
													type="text"
													placeholder=""
													value={
														answered[
															i
														].answer
													}
													onChange={(
														event
													) => {
														let answers =
															answered;
														answers[
															i
														] = {
															question:
																e.order,
															answer: event
																.target
																.value,
														};
														setAnswered(
															[
																...answers,
															]
														);
													}}
												/>
											</div>
										)}
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
				onClick={() => setMVModalActive(false)}
				className="modal-close is-large"
				aria-label="close"></button>
		</div>
	);
};
