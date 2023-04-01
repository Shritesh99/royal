import { gql } from "@apollo/client";
export default gql`
	query fslsmQuestions {
		fslsmQuestions {
			id
			text
			order
			choices {
				id
				text
			}
		}
	}
`;
