import Link from "next/link";

export const Card = (props) => {
	return (
		<Link className="button m-3 card" href={props.link} shallow={true}>
			<p className="is-size-5">{props.text}</p>
		</Link>
	);
};
