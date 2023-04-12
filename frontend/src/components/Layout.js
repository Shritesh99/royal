import { Header } from "./Header";
import { Footer } from "./Footer";

export const Layout = ({ children }) => {
	return (
		<section className="hero is-fullheight has-background-white-bis">
			<Header />
			{children}
			<Footer />
		</section>
	);
};
