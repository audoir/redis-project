from models import TopicEnum


# calculate F1 scores from confusion matrix data
def calculate_f1_scores(
    true_labels: list[TopicEnum], predicted_labels: list[TopicEnum]
) -> tuple[float, float]:
    tp = {topic: 0 for topic in TopicEnum}
    fp = {topic: 0 for topic in TopicEnum}
    fn = {topic: 0 for topic in TopicEnum}

    for true_label, pred_label in zip(true_labels, predicted_labels):
        if true_label == pred_label:
            tp[true_label] += 1
        else:
            fp[pred_label] += 1
            fn[true_label] += 1

    f1_scores = []
    for topic in TopicEnum:
        precision = (
            tp[topic] / (tp[topic] + fp[topic]) if (tp[topic] + fp[topic]) > 0 else 0
        )
        recall = (
            tp[topic] / (tp[topic] + fn[topic]) if (tp[topic] + fn[topic]) > 0 else 0
        )
        f1 = (
            2 * (precision * recall) / (precision + recall)
            if (precision + recall) > 0
            else 0
        )
        f1_scores.append(f1)

    # macro F1: average of all class F1 scores
    macro_f1 = sum(f1_scores) / len(f1_scores)

    # micro F1: global precision and recall (equal accuracy for multi-class)
    total_tp = sum(tp.values())
    total_fp = sum(fp.values())
    total_fn = sum(fn.values())

    micro_precision = (
        total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
    )
    micro_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
    micro_f1 = (
        2 * (micro_precision * micro_recall) / (micro_precision + micro_recall)
        if (micro_precision + micro_recall) > 0
        else 0
    )

    return macro_f1, micro_f1
