// Session service for managing sessions

export interface SessionMaterial {
  id: string;
  name: string;
  type: 'file' | 'link' | 'text';
  url?: string;
  content?: string;
  file?: File;
}

export interface Session {
  id: string;
  title: string;
  course: string;
  courseCode: string;
  instructor: string;
  instructorId?: string;
  date: string;
  time: string;
  startTime: string;
  endTime: string;
  duration: string;
  description: string;
  status: 'live' | 'upcoming' | 'completed';
  participants?: number;
  expectedParticipants?: number;
  engagement?: number;
  type: 'live' | 'scheduled' | 'recorded';
  recordingAvailable?: boolean;
  materials?: SessionMaterial[];
  createdAt?: string;
  updatedAt?: string;
}

class SessionService {
  private sessions: Session[] = [];
  private storageKey = 'learning_platform_sessions';

  constructor() {
    this.loadSessions();
    // Initialize with default sessions if empty
    if (this.sessions.length === 0) {
      this.initializeDefaultSessions();
    }
  }

  private initializeDefaultSessions() {
    const defaultSessions: Session[] = [
      {
        id: '1',
        title: 'Machine Learning: Neural Networks',
        course: 'Machine Learning Fundamentals',
        courseCode: 'CS301',
        instructor: 'Dr. Jane Smith',
        instructorId: 'instructor1',
        date: '2023-10-15',
        time: '14:00-15:30',
        startTime: '14:00',
        endTime: '15:30',
        duration: '90 min',
        description: 'Introduction to neural networks and their applications',
        status: 'live',
        participants: 32,
        engagement: 88,
        type: 'live'
      },
      {
        id: '2',
        title: 'Database Design: Normalization',
        course: 'Database Systems',
        courseCode: 'CS202',
        instructor: 'Prof. John Doe',
        instructorId: 'instructor2',
        date: '2023-10-16',
        time: '10:00-12:00',
        startTime: '10:00',
        endTime: '12:00',
        duration: '120 min',
        description: 'Understanding database normalization techniques',
        status: 'upcoming',
        participants: 28,
        expectedParticipants: 35,
        type: 'scheduled'
      },
      {
        id: '3',
        title: 'Advanced Programming: Design Patterns',
        course: 'Advanced Programming Techniques',
        courseCode: 'CS304',
        instructor: 'Dr. Maria Rodriguez',
        instructorId: 'instructor3',
        date: '2023-10-12',
        time: '15:00-16:30',
        startTime: '15:00',
        endTime: '16:30',
        duration: '90 min',
        description: 'Exploring common design patterns in software development',
        status: 'completed',
        participants: 25,
        engagement: 82,
        type: 'recorded',
        recordingAvailable: true
      },
      {
        id: '4',
        title: 'Data Structures: Trees and Graphs',
        course: 'Data Structures and Algorithms',
        courseCode: 'CS201',
        instructor: 'Prof. David Chen',
        instructorId: 'instructor4',
        date: '2023-10-11',
        time: '13:00-14:30',
        startTime: '13:00',
        endTime: '14:30',
        duration: '90 min',
        description: 'Deep dive into tree and graph data structures',
        status: 'completed',
        participants: 38,
        engagement: 75,
        type: 'recorded',
        recordingAvailable: true
      },
      {
        id: '5',
        title: 'Web Development: Frontend Frameworks',
        course: 'Web Development',
        courseCode: 'CS305',
        instructor: 'Dr. Alex Johnson',
        instructorId: 'instructor5',
        date: '2023-10-18',
        time: '11:00-12:30',
        startTime: '11:00',
        endTime: '12:30',
        duration: '90 min',
        description: 'Introduction to modern frontend frameworks',
        status: 'upcoming',
        participants: 0,
        expectedParticipants: 30,
        type: 'scheduled'
      }
    ];

    this.sessions = defaultSessions;
    this.saveSessions();
  }

  private loadSessions() {
    try {
      const stored = localStorage.getItem(this.storageKey);
      if (stored) {
        this.sessions = JSON.parse(stored);
      }
    } catch (error) {
      console.error('Error loading sessions from localStorage:', error);
    }
  }

  private saveSessions() {
    try {
      // Don't save file objects to localStorage
      const sessionsToSave = this.sessions.map(session => ({
        ...session,
        materials: session.materials?.map(m => ({
          ...m,
          file: undefined // Remove file objects before saving
        }))
      }));
      localStorage.setItem(this.storageKey, JSON.stringify(sessionsToSave));
    } catch (error) {
      console.error('Error saving sessions to localStorage:', error);
    }
  }

  getAllSessions(): Session[] {
    return [...this.sessions];
  }

  getSessionById(id: string): Session | undefined {
    return this.sessions.find(s => s.id === id);
  }

  createSession(sessionData: Omit<Session, 'id' | 'createdAt' | 'updatedAt'>, instructorName: string, instructorId?: string): Session {
    const newSession: Session = {
      ...sessionData,
      id: Date.now().toString(),
      instructor: instructorName,
      instructorId: instructorId || 'current-user',
      time: `${sessionData.startTime}-${sessionData.endTime}`,
      status: this.getSessionStatus(sessionData.date, sessionData.startTime, sessionData.endTime),
      participants: 0,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    this.sessions.push(newSession);
    this.saveSessions();
    return newSession;
  }

  updateSession(id: string, sessionData: Partial<Session>): Session | null {
    const index = this.sessions.findIndex(s => s.id === id);
    if (index === -1) return null;

    const updatedSession: Session = {
      ...this.sessions[index],
      ...sessionData,
      id, // Ensure ID doesn't change
      time: sessionData.startTime && sessionData.endTime 
        ? `${sessionData.startTime}-${sessionData.endTime}` 
        : this.sessions[index].time,
      status: sessionData.date && sessionData.startTime && sessionData.endTime
        ? this.getSessionStatus(sessionData.date, sessionData.startTime, sessionData.endTime)
        : this.sessions[index].status,
      updatedAt: new Date().toISOString()
    };

    this.sessions[index] = updatedSession;
    this.saveSessions();
    return updatedSession;
  }

  deleteSession(id: string): boolean {
    const index = this.sessions.findIndex(s => s.id === id);
    if (index === -1) return false;

    this.sessions.splice(index, 1);
    this.saveSessions();
    return true;
  }

  private getSessionStatus(date: string, startTime: string, endTime: string): 'live' | 'upcoming' | 'completed' {
    const now = new Date();
    const sessionDate = new Date(date);
    const [startHour, startMin] = startTime.split(':').map(Number);
    const [endHour, endMin] = endTime.split(':').map(Number);

    sessionDate.setHours(startHour, startMin, 0, 0);
    const endDate = new Date(date);
    endDate.setHours(endHour, endMin, 0, 0);

    if (now < sessionDate) {
      return 'upcoming';
    } else if (now >= sessionDate && now <= endDate) {
      return 'live';
    } else {
      return 'completed';
    }
  }

  // Update session status based on current time
  updateSessionStatuses() {
    this.sessions = this.sessions.map(session => {
      const status = this.getSessionStatus(session.date, session.startTime, session.endTime);
      if (status !== session.status) {
        return { ...session, status, updatedAt: new Date().toISOString() };
      }
      return session;
    });
    this.saveSessions();
  }
}

// Export singleton instance
export const sessionService = new SessionService();

// Update session statuses periodically
setInterval(() => {
  sessionService.updateSessionStatuses();
}, 60000); // Update every minute

