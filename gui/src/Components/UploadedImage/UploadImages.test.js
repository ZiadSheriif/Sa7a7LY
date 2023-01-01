import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import TestingComponent from "Features/Post/TestingComponent";

// Import components
import UploadedImage from "./UploadedImage";

const mockFile = {
  name: "test1.jpg",
  size: 1000,
  type: "image/jpeg",
  lastModified: 1620000000000,
  uploadDate: 1620000000000,
  preview: "https://preview1.jpg",
  src: "https://src1.jpg",
};

const mockDeleteFile = jest.fn();
const mockHandleClick = jest.fn();


describe("Uploaded images", () => {
  window.URL.revokeObjectURL = jest.fn();
  it("should render Uploaded image", () => {
    render(
      <TestingComponent>
        <UploadedImage
          selectedImageId={null}
          file={mockFile}
          handleClick={mockHandleClick}
          deleteFile={mockDeleteFile}
          id={1}
          isSelected={false}
        />
      </TestingComponent>
    );
  });

  it("should render Uploaded image components", async () => {
    render(
      <TestingComponent>
        <UploadedImage
          selectedImageId={null}
          file={mockFile}
          handleClick={mockHandleClick}
          deleteFile={mockDeleteFile}
          id={1}
          isSelected={false}
        />
      </TestingComponent>
    );
    expect(mockHandleClick).toBeCalledTimes(1);
    const image = screen.getByAltText("uploaded preview");
    expect(image).toBeInTheDocument();
    expect(screen.queryByRole("button")).toBe(null);
    fireEvent.mouseOver(image);
    const deleteBtn = screen.getByTestId("delete-button");
    expect(deleteBtn).toBeInTheDocument();
  });

  it("should be able to delete image", async () => {
    render(
      <TestingComponent>
        <UploadedImage
          selectedImageId={null}
          file={mockFile}
          handleClick={mockHandleClick}
          deleteFile={mockDeleteFile}
          id={1}
          isSelected={false}
        />
      </TestingComponent>
    );
    const image = screen.getByAltText("uploaded preview");
    fireEvent.mouseOver(image);
    const deleteBtn = screen.getByTestId("delete-button");
    fireEvent.click(deleteBtn);
    expect(mockDeleteFile).toBeCalledTimes(1);
  });

    it("should be able to select image", async () => {
      render(
        <TestingComponent>
          <UploadedImage
            selectedImageId={null}
            file={mockFile}
            handleClick={mockHandleClick}
            deleteFile={mockDeleteFile}
            id={1}
            isSelected={false}
          />
        </TestingComponent>
      );
      const image = screen.getByAltText("uploaded preview");
      fireEvent.click(image);
      expect(mockHandleClick).toBeCalledTimes(2);
    });
});
