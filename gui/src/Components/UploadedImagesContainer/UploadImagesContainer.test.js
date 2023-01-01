import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import TestingComponent from "Features/Post/TestingComponent";

// Import components
import UploadedImagesContainer from "./UploadedImagesContainer";

const mockFiles = [
  {
    name: "test1.jpg",
    size: 1000,
    type: "image/jpeg",
    lastModified: 1620000000000,
    uploadDate: 1620000000000,
    preview: "https://preview1.jpg",
    src: "https://src1.jpg",
  },
];


const mockSetFiles = jest.fn();
const mockSetSelectedImageId = jest.fn();

describe("Uploaded images container", () => {
  it("should render without crashing", () => {
    render(
      <TestingComponent>
        <UploadedImagesContainer
          files={[]}
          setFiles={mockSetFiles}
          setSelectedImageId={mockSetSelectedImageId}
        />
      </TestingComponent>
    );
    expect(screen.queryByTestId("upload-icon")).not.toBeInTheDocument();
  });
  it("should render without crashing with images", () => {
    render(
      <TestingComponent>
        <UploadedImagesContainer
          files={mockFiles}
          setFiles={mockSetFiles}
          setSelectedImageId={mockSetSelectedImageId}
        />
      </TestingComponent>
    );
    expect(screen.getByTestId("upload-icon")).toBeInTheDocument();
  });
});
