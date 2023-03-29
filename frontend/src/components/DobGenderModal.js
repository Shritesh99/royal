import "react-day-picker/dist/style.css";
import { useState } from "react";
import { useRecoilState } from "recoil";
import { ErrorAtom, DobGenderModalAtom } from "../atoms";
import { useMutation } from "@apollo/client";
import { AddDobGender } from "../gql";

export const DobGenderModal = () => {
	const [date, setDate] = useState();
	const [gender, setGender] = useState("male");
	const [err, setErr] = useRecoilState(ErrorAtom);
	const [dobGenderModalActtive, setDobGenderModal] =
		useRecoilState(DobGenderModalAtom);

	const [setDobGender] = useMutation(AddDobGender, {
		onCompleted: (data) => {
			if (data.addDobGender && data.addDobGender.success)
				setDobGenderModal(false);
		},
		onError: (error) => {
			setErr(error.message);
		},
	});

	const onSubmit = () => {
		if (!date) return setErr("No Date of Birth Selected");
		setDobGender({
			variables: {
				dob: date,
				gender: gender,
			},
		});
	};
	const maxDate = () => {
		var today = new Date();
		var dd = today.getDate();
		var mm = today.getMonth() + 1; //January is 0!
		var yyyy = today.getFullYear();
		if (dd < 10) {
			dd = "0" + dd;
		}
		if (mm < 10) {
			mm = "0" + mm;
		}
		return yyyy + "-" + mm + "-" + dd;
	};
	return (
		<div className={`modal ${dobGenderModalActtive ? "is-active" : ""}`}>
			<div className="modal-background"></div>
			<div className="modal-content">
				<section className="box">
					<p className="field is-size-3">
						One Last thing before starting
					</p>
					<div className="field is-horizontal">
						<div className="field-label is-normal">
							<label className="label">
								Date of Birth
							</label>
						</div>
						<div className="field-body">
							<div className="field">
								<p className="control">
									<input
										className="input"
										type="Date"
										onChange={(e) =>
											setDate(e.target.value)
										}
										max={`${maxDate()}`}
									/>
								</p>
							</div>
						</div>
					</div>

					<div className="field is-horizontal">
						<div className="field-label is-normal">
							<label className="label">Gender</label>
						</div>
						<div className="field-body">
							<div className="field">
								<div className="select">
									<select
										onChange={(e) =>
											setGender(e.target.value)
										}>
										<option value="male">
											Male
										</option>
										<option value="female">
											Female
										</option>
									</select>
								</div>
							</div>
						</div>
					</div>
					<div className="field is-horizontal">
						<div className="field-label is-normal">
							<button
								className="button is-primary"
								onClick={() => onSubmit()}>
								Submit
							</button>
						</div>
					</div>
				</section>
			</div>
			<button
				onClick={() => setDobGenderModal(false)}
				className="modal-close is-large"
				aria-label="close"></button>
		</div>
	);
};
