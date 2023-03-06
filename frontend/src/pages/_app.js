import "@/styles/globals.css";
import { useEffect } from "react";
import { useRecoilState, RecoilRoot } from "recoil";
import { LoadingAtom } from "../atoms";
import { Layout, Loading } from "../components";

const Application = ({ Component, pageProps }) => {
	const [loading, setLoading] = useRecoilState(LoadingAtom);
	useEffect(() => {
		setLoading(false);
	}, []);
	if (loading) return <Loading />;
	return (
		<RecoilRoot>
			<div className="hero-body is-align-items-flex-start container">
				<Component {...pageProps} />
			</div>
		</RecoilRoot>
	);
};

export default function App({ Component, pageProps }) {
	return (
		<RecoilRoot>
			<Layout>
				<Application Component={Component} pageProps={pageProps} />
			</Layout>
		</RecoilRoot>
	);
}
