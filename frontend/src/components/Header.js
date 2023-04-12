import Link from "next/link";
import { googleLogout } from "@react-oauth/google";
import { useRecoilState, useRecoilValue } from "recoil";
import { useRouter } from "next/router";
import { AuthAtom, isLoggedInSelector, FSLSMQuestionModalAtom } from "../atoms";

export const Header = () => {
	const router = useRouter();
	const [auth, setAuth] = useRecoilState(AuthAtom);
	const isLoggedIn = useRecoilValue(isLoggedInSelector);
	const [getFSLSMQuestionModalActive, setFSLSMQuestionModalActive] =
		useRecoilState(FSLSMQuestionModalAtom);
	const signOut = () => {
		googleLogout();
		setAuth(null);
		localStorage.clear();
	};
	return (
		<div className="hero-head">
			<header className="navbar has-background-primary">
				<div className="container">
					<div className="navbar-brand">
						<Link
							href="/"
							shallow={true}
							className="navbar-item has-text-primary-light">
							<p className="is-size-3">GRE Application</p>
						</Link>
					</div>
					{isLoggedIn ? (
						<div className="navbar-end">
							<div className="navbar-item has-dropdown is-hoverable is-align-items-center">
								<figure className="image box m-3">
									{auth.picture !== null ? (
										<img
											className="is-rounded"
											src={auth.picture}
										/>
									) : (
										<i className="fa-regular fa-user" />
									)}
								</figure>
								<div className="navbar-dropdown is-right">
									<a className="navbar-item button is-white">
										Profile
									</a>
									<button
										className="navbar-item button is-white"
										onClick={() =>
											setFSLSMQuestionModalActive(
												true
											)
										}>
										Set Learning style
									</button>
									<hr className="navbar-divider" />
									<a
										className="navbar-item button is-inverted is-danger"
										onClick={() => signOut()}>
										Sign Out
									</a>
								</div>
							</div>
						</div>
					) : (
						<></>
					)}
				</div>
			</header>
		</div>
	);
};
