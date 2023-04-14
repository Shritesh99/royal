import { gql } from "@apollo/client";
export default gql`
	mutation AddMotivationquestionsResponse($res: [MotivationQuestionInput]) {
		addMotivationquestionsResponse(response: $res) {
			success
		}
	}
`;
