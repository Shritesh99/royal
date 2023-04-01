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

	return <>Hello World!!</>;
}
