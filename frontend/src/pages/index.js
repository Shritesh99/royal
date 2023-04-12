import { useRecoilState, useRecoilValue } from "recoil";
import { useRouter } from "next/router";
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
			if (!auth.dob || !auth.gender) return setDobGenderModal(true);
			if (!auth.ls && auth.ls !== "")
				return setFSLSMQuestionModalActive(true);
		}
	}, [isLoggedIn]);

	const startTest = () => {
		router.push("/exam");
	};
	return (
		<div className="columns is-align-items-center container is-fullhd is-widescreen mx-3">
			<div className="column is-two-fifths">
				<div className="title is-1">Take test today!</div>
				<button
					className="button is-info"
					onClick={() => startTest()}>
					<span>Start Test</span>
				</button>
			</div>
			<div className="column is-three-fifths">
				<figure className="image">
					<Image src={img} alt="img" width={500} />
				</figure>
			</div>
		</div>
	);
}
