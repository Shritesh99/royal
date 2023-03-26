import "@/styles/globals.css";
import "react-toastify/dist/ReactToastify.css";

import { GoogleOAuthProvider } from "@react-oauth/google";
import { useEffect, useState } from "react";
import { useRecoilValue, RecoilRoot, useRecoilState } from "recoil";
import { LoadingAtom, isEmptyErrorSelector } from "../atoms";
import { Layout, Loading } from "../components";
import { ToastContainer, toast } from "react-toastify";

const Application = ({ Component, pageProps }) => {
	const [loading, setLoading] = useRecoilState(LoadingAtom);
	const err = useRecoilValue(isEmptyErrorSelector);

	useEffect(() => {
		setLoading(false);
	}, []);

	useEffect(() => {
		if (err) {
			toast.error(err);
		}
	});
	if (loading) return <Loading />;
	return (
		<>
			<ToastContainer />
			<div className="hero-body container">
				<Component {...pageProps} />
			</div>
		</>
	);
};

export default function App({ Component, pageProps }) {
	return (
		<RecoilRoot>
			<GoogleOAuthProvider
				clientId={process.env.NEXT_PUBLIC_GOOGLE_OAUTH_CLIENT_ID}>
				<Layout>
					<Application
						Component={Component}
						pageProps={pageProps}
					/>
				</Layout>
			</GoogleOAuthProvider>
		</RecoilRoot>
	);
}
