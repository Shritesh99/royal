import { useEffect, useState } from "react";
import { useGoogleLogin, hasGrantedAllScopesGoogle } from "@react-oauth/google";
import Image from "next/image";
import { useRecoilState } from "recoil";
import { useRouter } from "next/router";
import { ErrorAtom, LoadingAtom } from "../atoms";
import { Constants } from "../utils";
import img from "../../public/images/19197921.jpg";

export default function Auth() {
	const [loading, setLoading] = useRecoilState(LoadingAtom);
	const [err, setErr] = useRecoilState(ErrorAtom);
	useEffect(() => {
		setLoading(true);
		if (localStorage.getItem(Constants.GOOGLE_CLIENT_TOKEN)) {
			router.replace("/");
		}
		setLoading(false);
	}, []);
	const googleLogin = useGoogleLogin({
		scope: "https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/user.gender.read",
		onSuccess: (response) => {
			console.log(response);
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
				Constants.GOOGLE_CLIENT_TOKEN,
				credentialResponse.credential
			);
			router.push("/");
		},
	});

	const router = useRouter();
	return (
		<div className="container">
			<div className="columns is-align-items-center">
				<div className="column is-one-third ">
					<div className="title is-1">Let's get Started</div>
					<button class="button" onClick={() => googleLogin()}>
						<span class="icon">
							<i class="fab fa-google"></i>
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
