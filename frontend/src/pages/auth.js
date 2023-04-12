import { useEffect, useState } from "react";
import { useGoogleLogin } from "@react-oauth/google";
import Image from "next/image";
import { useRecoilState, useRecoilValue } from "recoil";
import { useRouter } from "next/router";
import { useMutation } from "@apollo/client";
import { ErrorAtom, LoadingAtom, AuthAtom, isLoggedInSelector } from "../atoms";
import { Constants } from "../utils";
import { SocialUserGQL } from "../gql";
import { User } from "../models";
import img from "../../public/images/19197921.jpg";

export default function Auth() {
	const router = useRouter();
	const [err, setErr] = useRecoilState(ErrorAtom);
	const [auth, setAuth] = useRecoilState(AuthAtom);
	const isLoggedIn = useRecoilValue(isLoggedInSelector);

	const [useSocialUser] = useMutation(SocialUserGQL, {
		onCompleted: (data) => {
			localStorage.setItem(
				Constants.ACCESS_TOKEN,
				data.socialUser.token
			);
			localStorage.setItem(
				Constants.REFERESH_TOKEN,
				data.socialUser.refreshToken
			);
			const user = new User(data.socialUser.user);
			setAuth(user);
			router.replace("/");
		},
		onError: (error) => {
			setErr(error.message);
		},
	});

	useEffect(() => {
		if (isLoggedIn) router.replace("/");
	}, []);
	const googleLogin = useGoogleLogin({
		onSuccess: (response) => {
			useSocialUser({
				variables: {
					token: response.access_token,
				},
			});
		},
	});

	return (
		<div className="container mx-3">
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
					<figure className="image">
						<Image src={img} alt="img" />
					</figure>
				</div>
			</div>
		</div>
	);
}
