import Image from "next/image";
import img from "../../public/images/404.jpg";

export default function Custom404() {
	return (
		<Image
			src={img}
			alt="img"
			width="0"
			height="0"
			sizes="100vw"
			style={{ width: "100%", height: "auto" }}
		/>
	);
}
