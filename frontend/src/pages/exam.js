import { useState, useEffect } from "react";
import { useLazyQuery } from "@apollo/client";
import { Loading } from "../components";
import { Test } from "../gql";
import { ErrorAtom, isLoggedInSelector, AuthAtom } from "../atoms";
import { useRecoilValue, RecoilRoot, useRecoilState } from "recoil";
import { useTimer } from "react-timer-hook";

const Field = (props) => {
	return (
		<div className="block">
			<input type="radio" />
			<label className="radio">{props.c.text}</label>
		</div>
	);
};
const Step = ({ q, i, seconds, minutes, active }) => {
	console.log(active);
	return (
		<div
			className={`column is-four-fifths ${
				active === i ? "" : "is-hidden"
			}`}>
			<p className="title">{q.text}</p>
			<div className="block">
				<div className="control">
					{q.choices.map((c) => (
						<Field
							name={c.id}
							key={c.id}
							label={c.text}
							c={c}
						/>
					))}
				</div>
			</div>
		</div>
	);
};
export default function Exam() {
	const [loading, setLoading] = useState(true);
	const isLoggedIn = useRecoilValue(isLoggedInSelector);
	const [err, setErr] = useRecoilState(ErrorAtom);
	const [testID, setTestId] = useState("");
	const [questions, setQuestions] = useState([]);

	const [active, setActive] = useState(0);

	const {
		seconds,
		minutes,
		hours,
		days,
		isRunning,
		start,
		pause,
		resume,
		restart,
	} = useTimer({
		expiryTimestamp: new Date().setSeconds(new Date().getMinutes() + 30),
		onExpire: () => console.warn("onExpire called"),
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
			setLoading(false);
			setActive(data.test.questions[0].id);
		},
		onError: (error) => {
			setErr(error);
			setLoading(false);
		},
	});

	if (loading) return <Loading />;
	return (
		<form
			className="box container is-fullhd is-widescreen is-flex is-flex-direction-column is-align-self-stretch is-justify-content-space-between"
			onSubmit={(e) => {
				e.preventDefault();
			}}>
			<div className="card-content">
				<div className="columns">
					{questions ? (
						questions.map((q, i) => (
							<Step
								q={q}
								i={i}
								key={q.id}
								seconds={seconds}
								minutes={minutes}
							/>
						))
					) : (
						<></>
					)}
					<div className="column is-flex is-justify-content-center">
						<div style={{ fontSize: "50px" }}>
							<span>{minutes}</span>:<span>{seconds}</span>
						</div>
					</div>
				</div>
			</div>
			<footer class="card-footer">
				<div className="card-footer-item">
					<button
						className="button is-full is-fullwidth is-warning"
						type="button">
						Previous
					</button>
				</div>
				<div className="card-footer-item">Question </div>
				<div className="card-footer-item">
					<button
						className="button is-full is-primary is-fullwidth"
						type="submit">
						Next
					</button>
				</div>
			</footer>
		</form>
	);
}
