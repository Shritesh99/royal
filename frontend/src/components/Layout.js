import { Header } from "./Header";
import { Footer } from "./Footer";

export const Layout = ({ children }) => {
	return (
		<section className="hero is-fullheight">
			<Header />
			{children}
			<Footer />
		</section>
	);
};
