import { render, screen, fireEvent } from "@testing-library/react";
import TestingComponent from "Features/Post/TestingComponent";

// Import components
import ImageAndVideoForm from "./ImageAndVideoForm";

const mockSubmitPost = jest.fn();

jest.mock("Features/Post/Services/getFlairs", () => (fetchData, auth) => {});

describe("Image and video form", () => {

  it("should be able to render title and post button", async () => {
    render(
      <TestingComponent>
        <ImageAndVideoForm submitPost={mockSubmitPost} />
      </TestingComponent>
    );
    expect(screen.getByPlaceholderText("Title")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Post" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Cancel" })).toBeInTheDocument();
  });

  it("should be able to type into title", () => {
    render(
      <TestingComponent>
        <ImageAndVideoForm submitPost={mockSubmitPost} />
      </TestingComponent>
    );
    const titleInput = screen.getByPlaceholderText("Title");
    fireEvent.click(titleInput);
    fireEvent.change(titleInput, { target: { value: "Test title" } });
    expect(titleInput.value).toBe("Test title");
  });

  it("should be able to type only 300 character in title", () => {
    render(
      <TestingComponent>
        <ImageAndVideoForm submitPost={mockSubmitPost} />
      </TestingComponent>
    );
    const titleInput = screen.getByPlaceholderText("Title");
    fireEvent.click(titleInput);
    fireEvent.change(titleInput, { target: { value: "T".repeat(300) + "a" } });
    expect(titleInput.value).toBe("");
  });

  it("should have disabled post button", () => {
    render(
      <TestingComponent>
        <ImageAndVideoForm submitPost={mockSubmitPost} />
      </TestingComponent>
    );
    const submitBtn = screen.getByRole("button", { name: "Post" });
    fireEvent.click(submitBtn);
    expect(submitBtn).toBeDisabled();
  });
});
