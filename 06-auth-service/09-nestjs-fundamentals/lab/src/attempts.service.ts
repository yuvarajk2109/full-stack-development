import { Injectable } from "@nestjs/common";
import { fail } from "node:assert";

const attempts = [
  { username: "dave", outcome: "success" },
  { username: "erin", outcome: "fail" },
  { username: "dave", outcome: "fail" },
  { username: "frank", outcome: "success" },
];

@Injectable()
export class AttemptsService {
  // TODO 1: implement getSummary() to return { successCount, failCount },
  // counted from the attempts array above - identical logic to Module
  // 2/3's counting.
  getSummary() {
    let successCount = 0;
    let failCount = 0;
    for (const { outcome } of attempts) {
      if (outcome == 'success') {
        successCount++;
      } else {
        failCount++;
      }
    }
    return { successCount, failCount };
  }
}
