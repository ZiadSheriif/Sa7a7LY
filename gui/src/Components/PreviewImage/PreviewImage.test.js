import { render, screen, fireEvent } from "@testing-library/react";
import TestingComponent from "Features/Post/TestingComponent";

// Import components
import PreviewImage from "./PreviewImage";


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
  {
    name: "test2.jpg",
    size: 1000,
    type: "image/jpeg",
    lastModified: 1620000000000,
    uploadDate: 1220000000000,
    preview: "https://preview2.jpg",
    src: "https://src2.jpg",
  },
  {
    name: "test3.jpg",
    size: 1000,
    type: "video/mp4",
    lastModified: 1620000000000,
    uploadDate: 1320000000000,
    preview: "https://preview3.jpg",
    src: "https://src3.jpg",
  },
];
describe("Preview image", () => {
  window.URL.revokeObjectURL = jest.fn();
  it("should render Preview image", () => {
    render(
      <TestingComponent>
        <PreviewImage selectedImageId={null} files={mockFiles} />
      </TestingComponent>
    );
  });

  it("should not render image if no selected image", () => {
    render(
      <TestingComponent>
        <PreviewImage selectedImageId={null} files={mockFiles} />
      </TestingComponent>
    );
    window.URL.revokeObjectURL = jest.fn(() => "details");
    expect(screen.queryByAltText("selected")).not.toBeInTheDocument();
  });

  it("should render image if there is a selected image", () => {
    const { container } = render(
      <TestingComponent>
        <PreviewImage
          selectedImageId={`test1.jpg1620000000000`}
          files={mockFiles}
        />
      </TestingComponent>
    );
    window.URL.revokeObjectURL = jest.fn(() => "details");
    expect(screen.getByAltText("selected")).toBeInTheDocument();
    expect(screen.getAllByRole("textbox").length).toBe(2);
    expect(screen.getByPlaceholderText("Add a caption...")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Add a link...")).toBeInTheDocument();
    expect(screen.getByAltText(/selected/i).src).toBe("https://src1.jpg/");
    expect(screen.queryByAltText("selected").controls).toBeFalsy();
  });

  it("should be able to render videos", () => {
    const { container } = render(
      <TestingComponent>
        <PreviewImage
          selectedImageId={`test3.jpg1320000000000`}
          files={mockFiles}
        />
      </TestingComponent>
    );
    window.URL.revokeObjectURL = jest.fn(() => "details");
    expect(screen.getByTestId("image")).toBeInTheDocument();
    expect(screen.getByTestId("image").src).toBe("https://src3.jpg/");
    expect(screen.getByTestId("image").controls).toBeTruthy();
  });
});
