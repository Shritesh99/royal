import { gql } from "@apollo/client";
export default gql`
	query MotivationQuestions {
		motivationQuestions {
			id
			order
			text
		}
	}
`;
