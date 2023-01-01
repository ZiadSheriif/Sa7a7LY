import { render } from "@testing-library/react";

import TestingComponent from "Features/Post/TestingComponent";
import ImagesAndVideosTab from "./ImagesAndVideosTab";


describe("ImagesAndVideos tab", () => {
  it("renders ImagesAndVideos tab component", () => {
    render(
      <TestingComponent>
        <ImagesAndVideosTab />
      </TestingComponent>
    );
  });
});
