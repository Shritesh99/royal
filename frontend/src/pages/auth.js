import { useEffect, useState } from "react";
import { useGoogleLogin, hasGrantedAllScopesGoogle } from "@react-oauth/google";
import Image from "next/image";
import { useRecoilState, useRecoilValue } from "recoil";
import { useRouter } from "next/router";
import { ErrorAtom, LoadingAtom, AuthAtom, isLoggedInSelector } from "../atoms";
import { Constants } from "../utils";
import img from "../../public/images/19197921.jpg";

export default function Auth() {
	const router = useRouter();
	const [err, setErr] = useRecoilState(ErrorAtom);
	const [auth, setAuth] = useRecoilState(AuthAtom);
	const isLoggedIn = useRecoilValue(isLoggedInSelector);
	useEffect(() => {
		if (isLoggedIn) router.replace("/");
	}, []);
	const googleLogin = useGoogleLogin({
		scope: "https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/user.gender.read",
		onSuccess: (response) => {
			const hasAccess = hasGrantedAllScopesGoogle(
				response,
				"https://www.googleapis.com/auth/user.birthday.read",
				"https://www.googleapis.com/auth/user.gender.read"
			);
			if (!hasAccess) {
				setErr("Not Given Proper Access");
				return;
			}
			localStorage.setItem(
				Constants.ACCESS_TOKEN,
				response.access_token
			);
			setAuth(response.access_token);
			router.replace("/");
		},
	});

	return (
		<div className="container">
			<div className="columns is-align-items-center">
				<div className="column is-one-third ">
					<div className="title is-1">Let's get Started</div>
					<button
						className="button"
						onClick={() => googleLogin()}>
						<span className="icon">
							<i className="fab fa-google"></i>
						</span>
						<span>Sign In With Google</span>
					</button>
				</div>
				<div className="column is-two-thirds">
					<Image src={img} alt="img" />
				</div>
			</div>
		</div>
	);
}
