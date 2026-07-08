import pandas as pd
from pathlib import Path
from typing import List, Tuple


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:

    orders_df = pd.read_csv(inputs_dir / "input_01.csv")
    box_sizes_df = pd.read_csv(inputs_dir / "input_02.csv")

    box_sizes = sorted(box_sizes_df['Box Size'].tolist(), reverse=True)

    output1_data = []

    output2_data = []

    def pack_order(order_num: int, order_size: int) -> Tuple[dict, List[Tuple[int, int]]]:
        remaining = order_size
        box_counts = {120: 0, 24: 0, 6: 0}
        boxes = []

        for box_size in box_sizes:
            num_boxes = remaining // box_size
            if num_boxes > 0:
                box_counts[box_size] = num_boxes
                for _ in range(num_boxes):
                    boxes.append((box_size, box_size))
                remaining -= num_boxes * box_size

        if remaining > 0:
            smallest_box = min(box_sizes)
            boxes.append((smallest_box, remaining))
            box_counts[smallest_box] += 1

        return box_counts, boxes

    for _, row in orders_df.iterrows():
        order_num = int(row['Order Number'])
        order_size = int(row['Order Size'])

        box_counts, boxes = pack_order(order_num, order_size)

        output1_data.append({
            'Order Number': order_num,
            'Order Size': order_size,
            'Boxes of 120': box_counts[120],
            'Boxes of 24': box_counts[24],
            'Boxes of 6': box_counts[6]
        })

        boxes_sorted = sorted(boxes, key=lambda x: x[1], reverse=True)

        size_counts = {}
        for box_size, _ in boxes_sorted:
            size_counts[box_size] = size_counts.get(box_size, 0) + 1

        box_number = 1
        for box_size, soaps_in_box in boxes_sorted:
            last_box_per_size = size_counts[box_size]

            output2_data.append({
                'Order Number': order_num,
                'Order Size': order_size,
                'Box Number': box_number,
                'Box Size': box_size,
                'Soaps in Box': soaps_in_box,
                'Last Box Per Box Size': last_box_per_size
            })
            box_number += 1

    output1_df = pd.DataFrame(output1_data)
    output2_df = pd.DataFrame(output2_data)

    return {
        'output_01.csv': output1_df,
        'output_02.csv': output2_df
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
