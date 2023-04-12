import { useState, useEffect } from "react";
import { Formiz, FormizStep, useForm, useField } from "@formiz/core";
import { useLazyQuery } from "@apollo/client";
import { Loading } from "../components";
import { Test } from "../gql";
import { ErrorAtom, isLoggedInSelector, AuthAtom } from "../atoms";
import { useRecoilValue, RecoilRoot, useRecoilState } from "recoil";

export const MyField = (props) => {
	const { setValue, value } = useField(props);

	return (
		<input
			type="radio"
			onChange={(e) => setValue(e.target.value)} // Update the value onChange
		/>
	);
};
export default function Exam() {
	const [loading, setLoading] = useState(true);
	const isLoggedIn = useRecoilValue(isLoggedInSelector);
	const [err, setErr] = useRecoilState(ErrorAtom);
	const myForm = useForm();
	const [testID, setTestId] = useState("");
	const [questions, setQuestions] = useState([]);

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
		},
		onError: (error) => {
			setErr(error);
			setLoading(false);
		},
	});

	const submitForm = (values) => {
		console.log(values);
	};
	if (loading) return <Loading />;
	return (
		<Formiz onValidSubmit={submitForm} connect={myForm}>
			<form
				noValidate
				onSubmit={myForm.submitStep}
				className="box container is-fullhd is-widescreen is-flex is-flex-direction-column is-align-self-stretch is-justify-content-space-between">
				{questions ? (
					questions.map((q, i) => (
						<FormizStep name={`step${i + 1}`} key={q.id}>
							<div className="card-content field">
								<p className="title">{q.text}</p>
								<div className="block">
									<div className="control">
										<fieldset>
											{q.choices.map((c) => (
												<label
													className="radio"
													key={c.id}>
													<MyField
														name="firstName"
														label={
															c.text
														}
														required="First Name is required"
													/>
													{c.text}
												</label>
											))}
										</fieldset>
									</div>
								</div>
							</div>
						</FormizStep>
					))
				) : (
					<></>
				)}
				<footer class="card-footer">
					<div className="card-footer-item">
						{!myForm.isFirstStep && (
							<button
								className="button is-full is-fullwidth is-warning"
								type="button"
								onClick={myForm.prevStep}>
								Previous
							</button>
						)}
					</div>
					<div className="card-footer-item">
						Question{" "}
						{(myForm.currentStep &&
							myForm.currentStep.index + 1) ||
							0}{" "}
						of {myForm.steps.length}
					</div>
					<div className="card-footer-item">
						<button
							className="button is-full is-primary is-fullwidth"
							type="submit"
							onClick={(e) => {
								myForm.isLastStep
									? myForm.submit(e)
									: myForm.nextStep();
							}}>
							{`${
								myForm.isLastStep
									? "Submit"
									: "Next Question"
							}`}
						</button>
					</div>
				</footer>
			</form>
		</Formiz>
	);
}
