import Link from "next/link";
import { googleLogout } from "@react-oauth/google";
import { useRecoilState, useRecoilValue } from "recoil";
import { useRouter } from "next/router";
import { AuthAtom, isLoggedInSelector } from "../atoms";

export const Header = () => {
	const router = useRouter();
	const [auth, setAuth] = useRecoilState(AuthAtom);
	const isLoggedIn = useRecoilValue(isLoggedInSelector);
	const signOut = () => {
		googleLogout();
		setAuth(null);
		localStorage.clear();
		router.replace("/auth");
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
								<i className="fa-regular fa-user m-3 box"></i>

								<div className="navbar-dropdown is-right">
									<a className="navbar-item">
										Profile
									</a>
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
