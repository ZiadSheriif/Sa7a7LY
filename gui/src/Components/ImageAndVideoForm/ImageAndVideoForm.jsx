// Import bootstrap components
import Form from "react-bootstrap/Form";

// Import components
import DragAndDropFile from "../DragDropFile/DragDropFile";
import PostFlagsWrapper from "../PostFlagsWrapper/PostFlagsWrapper";
import PostFormFooter from "../PostFormFooter/PostFormFooter";
import FlairModal from "../FlairModal/FlairModal";

// Import styled components
import {
  PostButton,
  StyledImageAndVideoFrom,
  CancelButton,
  SubmitButtons,
} from "./ImageAndVideoForm.styled";

// Import hooks
import { useState, useRef } from "react";

// Import contexts
import { useSubmitDestination } from "Features/Post/Contexts/submitDestination";
import { useCreatePostTitle } from "Features/Post/Contexts/createPostTitle";

// API services
import getPostFlairs from "Features/Post/Services/getFlairs";
import useFetchFunction from "Hooks/useFetchFunction";
import { useAuth } from "Features/Authentication/Contexts/Authentication";

// Import contexts
import { useCreatePostAttachments } from "Features/Post/Contexts/createPostAttachments";

// Import hooks
import { useEffect } from "react";
import { Spinner } from "react-bootstrap";

/**
 * Image and video form component (The form that appears when you click on the image and video tab in main section)
 * @param {Function} submitPost - Function to submit the post
 * @returns {React.Component} - Image and video form component (The form that appears when you click on the image and video tab in main section)
 */
const ImageAndVideoForm = ({ submitPost, isLoadingSubmit }) => {
  // State for flair modal
  const [modalShow, setModalShow] = useState(false);

  // State for flair
  const [flairIndex, setFlairIndex] = useState(null);

  // State for title
  const { createPostTitle, setCreatePostTitle } = useCreatePostTitle();

  // State for files
  const [files, setFiles] = useState([]);

  // Ref for title
  const titleRef = useRef(null);

  // Context for selected submit destination
  const { submitDestination } = useSubmitDestination();

  // Context for attachments
  const { createPostAttachments, setCreatePostAttachments } =
    useCreatePostAttachments();

  // const [flairs, error, isLoading, reload] = useFetch({
  //   axiosInstance: axios,
  //   method: "GET",
  //   url: "/flairs/",
  //   requestConfig: {
  //     headers: {
  //       "Content-Language": "en-US",
  //     },
  //   },
  // });
  // Fetch flairs
  let [flairs, error, isLoading, fetchData] = useFetchFunction();
  const auth = useAuth();
  useEffect(() => {
    if (submitDestination)
      getPostFlairs(fetchData, submitDestination._id, auth);
  }, [submitDestination]);

  /**
   * Handle title change
   *
   * @param {Event} e - Event
   */
  const handleTitleChange = (e) => {
    if (e.target.value.length <= 300) {
      setCreatePostTitle(e.target.value);
      titleRef.current.style.height = titleRef.current.scrollHeight + "px";
    }
  };

  /**
   * Handle key down
   *
   * @param {Event} e - Event
   */
  const handleKeyDown = (e) => {
    // Prevent enter key (new line)
    if (e.key === "Enter") {
      e.preventDefault();
    }
  };
  const onModalHide = () => {
    setModalShow(false);
    setFlairIndex(null);
  };

  /**
   * Handle form submit
   */
  const submitForm = () => {
    console.log("submit");
    setCreatePostAttachments(files);
    submitPost({ type: "image", attachments: files });
  };
  return (
    <>
      <FlairModal
        show={modalShow}
        onHide={onModalHide}
        flairIndex={flairIndex}
        setFlairIndex={setFlairIndex}
        flairList={flairs.flairs}
        error={error}
        isLoading={isLoading}
        postOrUser="post"
      />
      <StyledImageAndVideoFrom>
        <Form.Group className="title-group mb-3">
          <Form.Control
            ref={titleRef}
            as="textarea"
            placeholder="Title"
            value={createPostTitle}
            onChange={handleTitleChange}
            onKeyDown={handleKeyDown}
            rows={1}
            className="title-input"
            id="title"
          />
          <span>{createPostTitle.length}/300</span>
        </Form.Group>
        <DragAndDropFile files={files} setFiles={setFiles} />
        <PostFlagsWrapper flairHandler={setModalShow} />
        <SubmitButtons>
          <CancelButton variant="light">Cancel</CancelButton>
          <PostButton
            disabled={!submitDestination || !createPostTitle}
            onClick={submitForm}
            id="post"
          >
            {!isLoadingSubmit && "Post"}
            {isLoadingSubmit && <Spinner animation="border" variant="light" />}
          </PostButton>
        </SubmitButtons>
      </StyledImageAndVideoFrom>
      <PostFormFooter id={"ImageAndVideoForm"} />
    </>
  );
};

export default ImageAndVideoForm;
