import DeWatermark from "./";

const dewatermark = new DeWatermark();
const imageBuffer = await dewatermark.eraseWatermark(
    Buffer.from(
        await Bun.file("./shutterstock_image.jpg").arrayBuffer()
    )
);

const file = Bun.file("./result.jpg");
const writer = file.writer();
writer.write(imageBuffer);