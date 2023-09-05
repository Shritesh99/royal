import { gql } from "@apollo/client";
export default gql`
	mutation addDoBGEnder($dob: Date!, $gender: String!) {
		addDobGender(dob: $dob, gender: $gender) {
			success
		}
	}
`;
