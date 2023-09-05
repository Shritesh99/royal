import { gql } from "@apollo/client";
export default gql`
	mutation SubmitTest($testId: String, $res: [TestInteractionInput]) {
		submitTest(testId: $testId, response: $res) {
			success
		}
	}
`;
