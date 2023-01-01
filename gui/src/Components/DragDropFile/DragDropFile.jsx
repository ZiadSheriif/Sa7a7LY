// Import hooks
import React, { useEffect, useState } from "react";

// Import react dropzone
import { useDropzone } from "react-dropzone";

// Import components
import PreviewImage from "../PreviewImage/PreviewImage";
import UploadedImagesContainer from "../UploadedImagesContainer/UploadedImagesContainer";

// Import styled components
import {
  DragAndDropFrame,
  UploadButton,
  DragDropParagraph,
} from "./DragDropFile.styled";

/**
 * Drag and drop file component (The component that allows you to drag and drop files)
 *
 * @param {Array} files - Array of files (images and videos)
 * @param {Function} setFiles - Function to set files (images and videos)
 * @returns {React.Component} - Drag and drop file component (The component that allows you to drag and drop files)
 */
function DragAndDropFile({ files, setFiles }) {
  // State to store the selected image id
  const [selectedImageId, setSelectedImageId] = useState(null);

  // State to store whether the image loading is done or not
  const [isLoadingDone, setIsLoadingDone] = useState(false);

  // Use dropzone hook
  const { getRootProps, getInputProps, open } = useDropzone({
    // Disable click and keydown behavior
    noClick: true,
    noKeyboard: true,
    accept: {
      "image/*": [],
      "video/*": [],
    },
    onDrop: (acceptedFiles) => {
      const newFiles = [
        ...files,
        ...acceptedFiles.map((file) => {
          const reader = new FileReader();
          reader.onload = (x) => {
            Object.assign(file, {
              preview: URL.createObjectURL(file),
              src: x.target.result,
              uploadDate: new Date().getTime(),
            });
            if (reader.readyState === FileReader.DONE)
              setIsLoadingDone(() => !isLoadingDone);
          };
          reader.readAsDataURL(file);
          return file;
        }),
      ];
      setFiles(() => newFiles);
    },
  });

  useEffect(() => {
    // Make sure to revoke the data uris to avoid memory leaks, will run on unmount
    return () => files.forEach((file) => URL.revokeObjectURL(file.preview));
  });

  return (
    <div>
      <DragAndDropFrame {...getRootProps()} containFiles={files.length !== 0}>
        <input {...getInputProps()} />
        {files.length === 0 && (
          <DragDropParagraph>
            Drag And drop images or
            <UploadButton variant="light" onClick={open}>
              Upload
            </UploadButton>
          </DragDropParagraph>
        )}
        <UploadedImagesContainer
          files={files}
          setFiles={setFiles}
          open={open}
          selectedImageId={selectedImageId}
          setSelectedImageId={setSelectedImageId}
        />
      </DragAndDropFrame>
      {files.length > 1 && (
        <PreviewImage
          selectedImageId={selectedImageId}
          files={files}
          isLoadingDone={isLoadingDone}
        />
      )}
    </div>
  );
}

export default DragAndDropFile;
