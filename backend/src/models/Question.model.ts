// Mock Question model - in real app, this would use a database
const questions: Map<string, any> = new Map();

export class Question {
  static async findById(id: string) {
    return questions.get(id) || null;
  }

  static async create(data: any) {
    const question = {
      id: data.id || Date.now().toString(),
      ...data,
    };
    questions.set(question.id, question);
    return question;
  }
}

