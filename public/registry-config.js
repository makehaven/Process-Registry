/**
 * Deployment configuration for the participation layer.
 *
 * Everything here is public by design. The Firebase web apiKey is not a secret
 * — it identifies the project, and access is decided by firestore.rules plus the
 * Drupal-minted token. The OAuth client id is likewise public; PKCE is what
 * makes a browser client safe without a client secret.
 *
 * OAUTH_CLIENT_ID is the one value that has to be filled in by hand, because the
 * consumer is created in Drupal at /admin/config/services/consumer. Until it is
 * set, the page renders exactly as it did before — sign-in is hidden rather than
 * broken, so a half-finished setup never shows visitors a button that fails.
 */
export const DRUPAL_BASE_URL = "https://www.makehaven.org";

// Drupal consumer for this app. See SETUP.md → "Participation".
// Deliberately the same string as FIREBASE_APP_ID and the OAuth scope: consumers
// let you choose the client id, so one name is carried through rather than three.
export const OAUTH_CLIENT_ID = "process_registry";

// Scope requested at /oauth/authorize. `process_registry` narrows the grant;
// it does not replace the permission checks Drupal makes on the token route.
export const OAUTH_SCOPE = "openid email profile process_registry";

// Path segment on the bridge: /api/firebase-token/{app_id}
export const FIREBASE_APP_ID = "process_registry";

export const FIREBASE_CONFIG = {
  apiKey: "AIzaSyCyNEUxJiketZ3MCutuf4La75qHwYYb6ns",
  authDomain: "makehaven-process-registry.firebaseapp.com",
  projectId: "makehaven-process-registry",
  storageBucket: "makehaven-process-registry.firebasestorage.app",
  messagingSenderId: "1026475428349",
  appId: "1:1026475428349:web:4a234b8baa2dfa27907194",
};

/**
 * How far a vote can move a row.
 *
 * The base score is impact x how manual something still is, so it runs 1-20. A
 * cap of 5 lets the room overrule the arithmetic by a meaningful margin — enough
 * to lift a row several places — without letting a handful of early clicks bury
 * an I5 safety process nobody happened to vote on. Net votes, not raw counts:
 * three ups and two downs is a disagreement, not a mandate.
 */
export const VOTE_CAP = 5;
