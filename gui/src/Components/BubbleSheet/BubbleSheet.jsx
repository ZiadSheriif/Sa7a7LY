// Import components
import DragAndDropFile from "../DragDropFile/DragDropFile";
import CheckInput from "../CheckInput/CheckInput";

// Import styled components
import {
  PostButton,
  StyledImageAndVideoFrom,
  CancelButton,
  SubmitButtons,
} from "./BubbleSheet.styled";

// Import hooks
import { useState, useRef } from "react";

// Import hooks
import { Spinner } from "react-bootstrap";

/**
 * Image and video form component (The form that appears when you click on the image and video tab in main section)
 * @param {Function} submitPost - Function to submit the post
 * @returns {React.Component} - Image and video form component (The form that appears when you click on the image and video tab in main section)
 */
const BubbleSheet = ({ submitPost, isLoadingSubmit }) => {
  const [files, setFiles] = useState([]);

  /**
   * Handle form submit
   */
  const submitForm = () => {
    submitPost({ attachments: files});
  };
  return (
    <>
      <StyledImageAndVideoFrom>
        <DragAndDropFile files={files} setFiles={setFiles} />
        <SubmitButtons>
          <CancelButton variant="light">Cancel</CancelButton>
          <PostButton id="post" onClick={submitForm}>
            {!isLoadingSubmit && "Submit"}
            {isLoadingSubmit && <Spinner animation="border" variant="light" />}
          </PostButton>
        </SubmitButtons>
      </StyledImageAndVideoFrom>
    </>
  );
};

export default BubbleSheet;
