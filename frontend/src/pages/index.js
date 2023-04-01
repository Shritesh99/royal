import { useRecoilState, useRecoilValue } from "recoil";
import { useRouter } from "next/router";
import { useLazyQuery } from "@apollo/client";
import {
	LoadingAtom,
	isLoggedInSelector,
	DobGenderModalAtom,
	AuthAtom,
	FSLSMQuestionModalAtom,
} from "../atoms";
import { User } from "../models";
import { useEffect } from "react";
import img from "../../public/images/home.jpg";
import Image from "next/image";

export default function Home({ props }) {
	const router = useRouter();
	const isLoggedIn = useRecoilValue(isLoggedInSelector);
	const [loading, setLoading] = useRecoilState(LoadingAtom);
	const [dobGenderModalActtive, setDobGenderModal] =
		useRecoilState(DobGenderModalAtom);
	const [auth, setAuth] = useRecoilState(AuthAtom);
	const [getFSLSMQuestionModalActive, setFSLSMQuestionModalActive] =
		useRecoilState(FSLSMQuestionModalAtom);

	useEffect(() => {
		if (!isLoggedIn) {
			setAuth(null);
			setLoading(false);
			router.replace("/auth");
		} else {
			if (!auth.dob || !auth.gender) setDobGenderModal(true);
			if (!auth.ls && auth.ls !== "")
				setFSLSMQuestionModalActive(true);
		}
	}, [isLoggedIn]);

	const startTest = () => {};
	return (
		<div className="container">
			<div className="columns is-align-items-center">
				<div className="column is-one-third ">
					<div className="title is-1">Take test today!</div>
					<button className="button" onClick={() => startTest()}>
						<span>Start Test</span>
					</button>
				</div>
				<div className="column is-two-thirds">
					<figure className="image">
						<Image src={img} alt="img" width={500} />
					</figure>
				</div>
			</div>
		</div>
	);
}
