import { useEffect, useState } from "react";
import { GoogleLogin } from "@react-oauth/google";
import Image from "next/image";
import { useRecoilState } from "recoil";
import { useRouter } from "next/router";
import { ErrorAtom, LoadingAtom } from "../atoms";
import { Constants } from "../utils";

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
	const router = useRouter();
	return (
		<div className="container">
			<div className="columns is-align-items-center">
				<div className="column is-one-third ">
					<div className="title is-1">Let's get Started</div>
					<GoogleLogin
						onSuccess={(credentialResponse) => {
							localStorage.setItem(
								Constants.GOOGLE_CLIENT_TOKEN,
								credentialResponse.credential
							);
							router.push("/");
						}}
						onError={() => {
							setErr("Login Failed");
						}}
						useOneTap
						auto_select
					/>
				</div>
				<div className="column is-two-thirds">
					<Image
						src="/images/19197921.jpg"
						alt="img"
						width="0"
						height="0"
						sizes="100vw"
						style={{ width: "100%", height: "auto" }}
					/>
				</div>
			</div>
		</div>
	);
}
