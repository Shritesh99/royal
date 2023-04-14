import { useState, useEffect, useRef } from "react";
import { useLazyQuery, useMutation } from "@apollo/client";
import { Loading } from "../components";
import { Test, SubmitTest } from "../gql";
import { ErrorAtom, isLoggedInSelector, AuthAtom } from "../atoms";
import { useRecoilValue, RecoilRoot, useRecoilState } from "recoil";
import { useTimer } from "react-timer-hook";
import { useRouter } from "next/router";
import { Formik, Field, Form } from "formik";

export default function Exam() {
	const router = useRouter();
	const [loading, setLoading] = useState(true);
	const isLoggedIn = useRecoilValue(isLoggedInSelector);
	const [err, setErr] = useRecoilState(ErrorAtom);
	const [testID, setTestId] = useState("");
	const [questions, setQuestions] = useState([]);
	const [answered, setAnswered] = useState([]);
	const [active, setActive] = useState(0);
	const prevCountRef = useRef();
	const [timeTaken, setTimeTaken] = useState([]);

	const { seconds, minutes } = useTimer({
		expiryTimestamp: new Date().setSeconds(
			new Date().getSeconds() + 30 * 60
		),
		onExpire: () => router.replace("/"),
	});

	useEffect(() => {
		if (!isLoggedIn) {
			setAuth(null);
			setLoading(false);
			router.replace("/auth");
		}
	}, [isLoggedIn]);

	useEffect(() => {
		getQuestion({ variables: { testId: testID } });
	}, []);

	const [getQuestion] = useLazyQuery(Test, {
		onCompleted: (data) => {
			setTestId(data.test.testId);
			setQuestions(data.test.questions);
			const arr = Array(data.test.questions.length)
				.fill()
				.map(() => ({
					startTime: null,
					endTime: null,
				}));
			arr[0].startTime = Date.now();
			setTimeTaken(arr);
			setActive(0);
			prevCountRef.current = 0;
			setLoading(false);
		},
		onError: (error) => {
			setErr(error);
			setLoading(false);
		},
	});

	const [submitTest] = useMutation(SubmitTest, {
		onCompleted: (data) => {
			if (data.submitTest && data.submitTest.success)
				router.replace("/");
		},
		onError: (error) => {
			setErr(error.message);
		},
	});

	const changeRes = (value, isFront) => {
		const newTimes = [...timeTaken];
		const endTime = Date.now();
		newTimes[active].endTime = endTime;
		newTimes[active].duration = endTime - newTimes[active].startTime;

		newTimes[isFront ? active + 1 : active - 1].startTime = Date.now();

		if (value.choice === "") return;
		const arr = value.choice.split(",");
		setAnswered([
			...answered.filter((e) => e.questionId !== arr[0]),
			{
				questionId: arr[0],
				choiceId: arr[1],
				timeTaken: parseInt(newTimes[active].duration / 1000),
			},
		]);
		setTimeTaken(newTimes);
	};
	const onSubmit = (value) => {
		if (active !== questions.length - 1) {
			setActive(active + 1);
			changeRes(value, true);
			return;
		}
		submitTest({
			variables: { res: answered, testId: testID },
		});
	};

	if (loading) return <Loading />;
	return (
		<Formik
			initialValues={{
				choice: "",
			}}
			onSubmit={(value) => {
				onSubmit(value);
			}}>
			{({ values }) => (
				<Form className="box container is-fullhd is-widescreen is-flex is-flex-direction-column is-align-self-stretch is-justify-content-space-between">
					<div className="card-content">
						<div className="columns">
							{questions ? (
								questions.map((q, i) => (
									<div
										key={q.id}
										className={`column is-four-fifths ${
											active === i
												? ""
												: "is-hidden"
										}`}>
										<p
											id="my-radio-group"
											className="title">
											{q.text}
										</p>
										<div
											className="block"
											role="group"
											aria-labelledby="my-radio-group">
											{q.choices.map((c) => (
												<div
													className="block"
													key={c.id}>
													<label className="radio">
														<Field
															type="radio"
															name="choice"
															value={`${q.id},${c.id}`}
														/>
														{c.text}
													</label>
												</div>
											))}
										</div>
									</div>
								))
							) : (
								<></>
							)}
							<div className="column is-flex is-justify-content-center">
								<div style={{ fontSize: "50px" }}>
									<span>{minutes}</span>:
									<span>{seconds}</span>
								</div>
							</div>
						</div>
					</div>
					<footer className="card-footer">
						<div className="card-footer-item">
							<button
								className={`button is-full is-fullwidth is-warning ${
									active === 0 ? "is-hidden" : ""
								}`}
								type="button"
								onClick={() => {
									setActive(active - 1);
									changeRes(values, false);
								}}>
								Previous
							</button>
						</div>
						<div className="card-footer-item">{`Question ${
							active + 1
						} of ${questions.length}`}</div>
						<div className="card-footer-item">
							<button
								className="button is-full is-primary is-fullwidth"
								type="submit">{`${
								active === questions.length - 1
									? "Submit Test"
									: "Next Question"
							}`}</button>
						</div>
					</footer>
				</Form>
			)}
		</Formik>
	);
}
