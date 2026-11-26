export interface NotaryResult {
  exitCode: number;
  stdout: string;
  stderr: string;
  ok: boolean;
}

export declare const SDK_VERSION: string;

export declare class NotaryClient {
  constructor(binaryPath?: string);
  readonly binary: string;
  stamp(projectPath?: string, identity?: string | null): NotaryResult;
  verify(projectPath: string, proofPath: string): NotaryResult;
  verifyOts(
    projectPath: string,
    proofPath: string,
    opts?: { checkCalendar?: boolean; header?: string }
  ): NotaryResult;
  history(projectPath?: string): NotaryResult;
  license(action?: string | null, key?: string | null, json?: boolean): NotaryResult;
}

export declare function getNotaryBinary(): string | null;
export declare function platformBinaryName(): string | null;
